__spec__ = None  # Work around a weird issue when using debugger

if __name__ == '__main__':  # Needed for parallel SGF file download to work
  from dlgo.data.processor import GoDataProcessor

  processor = GoDataProcessor()
  features, labels = processor.load_go_data('train', 100)
