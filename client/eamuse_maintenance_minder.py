import datetime
import pytz


class EamuseMaintenanceMinder:

    def __init__(self, discord_client):
        self.client = discord_client

        self.eamuse_maintenance = {
            "normal": (
                datetime.time(hour=20, tzinfo=pytz.utc),
                datetime.time(hour=22, tzinfo=pytz.utc)
            ),
            "extended": (
                datetime.time(hour=17, tzinfo=pytz.utc),
                datetime.time(hour=22, tzinfo=pytz.utc)
            ),
            "us": (
                datetime.time(hour=12, tzinfo=pytz.utc),
                datetime.time(hour=17, tzinfo=pytz.utc)
            ),
        }

    async def get_eamuse_maintenance(self, message):
        """
        Gets eAmusement maintenance time.

        DDR (US Servers) - Third Monday of the month from 12 to 5 (?)
        Everything else - Sun-Thurs from 4 to 6. Third Monday 1 to 6

        Required:
        """

        if self.__is_extended_maintenance_time():
            ddr_message = self.__get_display_time("us")
            other_message = self.__get_display_time("extended")
        else:
            ddr_message = ":white_check_mark: - no maintenance today"
            other_message = self.__get_display_time("normal")

        await self.client.send_message(message.channel, f"DDR: {ddr_message}")
        await self.client.send_message(message.channel, f"Other: {other_message}")

    def __get_display_time(self, timing_type):
        """
        Get a display time for today's eAmusement maintenance time. Includes an
        emoji for if the current time is within that time.

        Uses the timing_types: "us", "normal", "extended" from self
        """
        today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        begin_datetime = datetime.datetime.combine(today.date(), self.eamuse_maintenance[timing_type][0])
        end_datetime = datetime.datetime.combine(today.date(), self.eamuse_maintenance[timing_type][1])
        if begin_datetime <= today <= end_datetime:
            emoji = ":x:"
        else:
            emoji = ":white_check_mark:"
        begin_time = begin_datetime.astimezone(pytz.timezone("America/New_York"))
        end_time = end_datetime.astimezone(pytz.timezone("America/New_York"))
        return f"{emoji} - {begin_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

    def __is_extended_maintenance_time(self):
        """
        This function returns true if this represents the Monday that Americans
        have to deal with maintenance.

        Maintenance is on the Third Tuesday in Japan.

        Gotchas:
            -The second Monday in America can be the Third Tuesday in Japan.
            -We literally don't care about this at all if it's Tuesday in
             in America, even if it's Tuesday in Japan
            -We DO care about it if it's Monday in America but still Monday in Japan

        :return: True if this is a Monday that Americans have to deal with maintenance
                 False if it's not
        """
        today_in_japan = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("Japan"))
        tomorrow_in_japan = today_in_japan + datetime.timedelta(days=1)
        today_in_eastern = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("America/New_York"))

        # If it's Monday in America, and either the third Tuesday or the Monday before that in Japan
        if today_in_eastern.weekday() == 0 and (
                (today_in_japan.weekday() == 1 and 15 <= today_in_japan.day <= 21) or (
                tomorrow_in_japan.weekday() == 1 and 15 <= tomorrow_in_japan.day <= 21)):
            return True
        return False
