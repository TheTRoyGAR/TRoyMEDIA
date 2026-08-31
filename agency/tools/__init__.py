from pathlib import Path
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool, FileReadTool
from agency.tools.safe_directory_tool import SafeDirectoryReadTool

search = SerperDevTool()
scrape = ScrapeWebsiteTool()
write = FileWriterTool()

_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
read_file = FileReadTool(base_dir=_PROJECT_ROOT)
# Not crewai_tools' DirectoryReadTool: that one does a raw, unfiltered
# os.walk() with no exclusions and can blow the context budget on a real
# repo (see TRoyGO's node_modules/.next incident, 2026-08-31).
list_dir = SafeDirectoryReadTool(root=_PROJECT_ROOT)
