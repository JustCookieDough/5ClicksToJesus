
class Link:
    start: int
    end: int

    def __init__(self, start_id: int, end_id: int):
        self.start = start_id
        self.end = end_id


class Page:
    page_id: int
    _namespace: int
    title: str
    _is_redirect: bool
    
    def __init__(self, page_id: int, namespace: int, title: str, is_redirect: bool) -> None:
        self.page_id = page_id
        self._namespace = namespace
        self.title = title
        self._is_redirect = is_redirect

    def __str__(self) -> str:
        return f"{self.page_id},{self._namespace},{self.title},{1 if self.is_redirect else 0}"
    
    def is_valid(self) -> bool:
        return self._namespace == 0 and not self._is_redirect
    
    def is_valid_redirect(self) -> bool:
        return self._namespace == 0 and self._is_redirect
    
    def is_ns0(self) -> bool:
        return self._namespace == 0
    

class DatabaseInfo:
    header_size: int
    pattern: str

    def __init__(self, header_size: int, pattern_string: str) -> None:
        self.pattern = pattern_string
        self.header_size = header_size


class Version:


    def __init__(self, version: str) -> None:
        if version == "1.41":
            self.links = DatabaseInfo(43, "(\d+),(\d+),'(.+?)',(\d+),")
            self.pages = DatabaseInfo(50, "(\d+),(\d+),'(.+?)',(\d+),")
            self.redirects = DatabaseInfo(40, "(\d+),([\d-]+),'(.+?)',")
        elif version == "1.15":
            self.links = DatabaseInfo(37, "(\d+),(\d+),'(.+?)'")
            self.pages = DatabaseInfo(47, "(\d+),(\d+),'(.+?)','.*',\d+,(\d+),")
            self.redirects = DatabaseInfo(37, "(\d+),([\d-]+),'(.+?)'")
        else:
            raise ValueError(f"MediaWiki version {version} is not supported.")