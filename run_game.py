import por.__main__
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:
        import por.level
        por.level.main()
        raise SystemExit

    por.__main__.main()
