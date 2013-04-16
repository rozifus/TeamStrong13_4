import por.__main__
import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print "Error: usage run_game.py <level>"
        print "If no level specified, level 'default' is loaded"
        sys.exit(1)
    
    if (len(sys.argv) == 2):
        levelname = sys.argv[1]
    else:
        levelname = "default"
    
    por.__main__.main(levelname)

