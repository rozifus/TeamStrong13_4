import por.main
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import por.demosound
        raise SystemExit

    por.main.run()

