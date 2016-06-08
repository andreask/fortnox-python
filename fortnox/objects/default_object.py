# coding=utf-8


class DefaultObject():
    item_url = None
    valid_search_params = ['page', 'limit', 'offset']

    def __str__(self):
        if self.id:
            return "%s" % self.id
        else:
            return ""

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.__str__())