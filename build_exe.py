import PyInstaller.__main__
import sys
import os
import shutil


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")


def build_executable():
    """Build the matrix calculator executable"""
    print("🔨 Building Matrix Calculator executable...")

    # Clean previous builds
    clean_build_dirs()

    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Build arguments
    args = [
        '--name=CalculadoraMatrices',
        '--onefile',
        '--windowed',
        '--distpath=dist',
        '--workpath=build',
        '--specpath=.',
        '--collect-all=customtkinter',
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--add-data=src;src',
        'main.py'
    ]

    # Add icon if it exists
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')
        print("🎨 Adding custom icon")

    try:
        print("📦 Starting PyInstaller build...")
        PyInstaller.__main__.run(args)

        # Check if build was successful
        exe_path = os.path.join('dist', 'CalculadoraMatrices.exe')
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"\n✅ Build completed successfully!")
            print(f"📁 Executable location: {exe_path}")
            print(f"📏 File size: {file_size:.1f} MB")
            print("\n🎉 Ready to distribute!")
            return True
        else:
            print("\n❌ Build failed: Executable not found")
            return False

    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False


if __name__ == "__main__":
    success = build_executable()

    if not success:
        print("\n💥 Build failed. Check the errors above.")
        sys.exit(1)

    print("\n🚀 Build process completed.")
