# Define variables
TARGET = Krita-Brush-Opacity-Docker.zip
DIR = brushOpacityDocker

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Zip target
$(TARGET): $(DIR)/* brushOpacityDocker.desktop LICENSE
	@echo $(info Creating zip archive...)
	@mkdir -p tmp/$(DIR)
	@cp -R $(DIR)/* tmp/$(DIR)/
	@cp LICENSE tmp/$(DIR)/
	@cp brushOpacityDocker.desktop tmp/
	@cd tmp && zip -r ../$(TARGET) .
	@rm -rf tmp
	@echo $(info Zip archive created: $(TARGET))

# Clean target
clean:
	@echo "Cleaning up..."
	@rm -f $(TARGET)
	@rm -rf tmp
	@echo "Cleanup complete."
