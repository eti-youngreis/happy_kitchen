class CourseType:
    MAIN = "מנה עיקרית"
    FIRST_COURSE = "מנה ראשונה"
    DESSERT = "קינוח"

    @classmethod
    def all(cls):
        return [cls.MAIN, cls.FIRST_COURSE, cls.DESSERT]

class DairyType:
    MEAT = "בשרי"
    DAIRY = "חלבי"
    PARVE = "פרווה"

    @classmethod
    def all(cls):
        return [cls.MEAT, cls.DAIRY, cls.PARVE]