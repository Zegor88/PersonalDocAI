import sys
from pathlib import Path
import streamlit.web.cli as stcli
from dotenv import load_dotenv

def main():
    """
    The main entry point for running the Streamlit app.
    This script handles setting up the correct Python path and launching Streamlit.
    """
    # Load environment variables from .env file
    load_dotenv()

    # The root of the project
    project_root = Path(__file__).parent
    # The path to the source code
    src_path = project_root / "src"

    # Add the source directory to the Python path
    sys.path.insert(0, str(src_path))

    # The path to the Streamlit app script
    app_file = src_path / "familydoc_ai" / "app.py"

    # Prepare arguments for Streamlit
    # This is equivalent to running `streamlit run src/familydoc_ai/app.py`
    # from the command line, but with the correct path context.
    args = [
        "streamlit",
        "run",
        str(app_file),
    ]

    # Replace the current process's arguments with Streamlit's arguments
    sys.argv = args
    
    # Run Streamlit's command line interface
    stcli.main()

if __name__ == "__main__":
    main() 