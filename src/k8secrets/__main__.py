import logging

logging.basicConfig(levle=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("HELLO")


if __name__ == "__main__":
    main()
