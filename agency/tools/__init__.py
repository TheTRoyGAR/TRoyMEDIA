from pathlib import Path
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool, FileReadTool, DirectoryReadTool

search = SerperDevTool()
scrape = ScrapeWebsiteTool()
write = FileWriterTool()

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
read_file = FileReadTool(base_dir=_PROJECT_ROOT)
list_dir = DirectoryReadTool(directory=_PROJECT_ROOT)
