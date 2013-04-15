import por.__main__
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:
        import por.level
        por.level.main()
        sys.exit(0)

    por.__main__.main()
