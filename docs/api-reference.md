# API Reference

## Core Classes

### InterfazGeneradorAudio

Main application class that handles the GUI and audio generation.

#### Constructor
`python
InterfazGeneradorAudio()
`

Creates the main application window and initializes all components.

#### Key Methods

##### crear_interfaz()
Sets up the user interface with all widgets and styling.

**Returns**: None

##### dividir_texto(texto, max_chars=1000)
Divides long text into manageable segments for audio generation.

**Parameters**:
- 	exto (str): Input text to divide
- max_chars (int): Maximum characters per segment

**Returns**: List of text segments

**Example**:
`python
app = InterfazGeneradorAudio()
segments = app.dividir_texto("Long text here...", 500)
`

##### crear_ssml(texto)
Creates SSML (Speech Synthesis Markup Language) for enhanced audio generation.

**Parameters**:
- 	exto (str): Text to convert to SSML

**Returns**: SSML formatted string

##### sync generar_audio_async()
Asynchronous method that handles the complete audio generation process.

**Returns**: None

**Raises**:
- Exception: Various exceptions related to file I/O or TTS errors

#### Key Attributes

##### Voice Configuration
- self.voz (tk.StringVar): Selected voice ID
- self.velocidad (tk.StringVar): Speech rate setting
- self.nombre_proyecto (tk.StringVar): Output project name
- self.modo_generacion (tk.StringVar): Generation mode ("unico" or "segmentos")

##### File Management
- self.carpeta_salida (str): Output directory path
- self.generando (bool): Generation status flag

##### UI Components
- self.text_area (scrolledtext.ScrolledText): Main text input area
- self.progress (ttk.Progressbar): Progress indicator
- self.status_label (tk.Label): Status message display

## Voice Constants

### Available Voices
`python
VOICES = [
    "es-MX-DaliaNeural",    # Mexico - Female
    "es-ES-AlvaroNeural",   # Spain - Male
    "es-ES-ElviraNeural",   # Spain - Female
    "es-AR-ElenaNeural",    # Argentina - Female
    "es-CO-SalomeNeural"    # Colombia - Female
]
`

### Speed Settings
`python
SPEEDS = ["-30%", "-20%", "-10%", "+0%", "+10%", "+20%"]
`

## Dependencies

### External Libraries
- dge-tts: Microsoft Edge Text-to-Speech API
- 	kinter: GUI framework (built-in with Python)
- syncio: Asynchronous I/O operations
- 	hreading: Thread management for non-blocking UI

### Standard Library Modules
- os: Operating system interface
- e: Regular expressions for text processing
- datetime: Date and time utilities

## Configuration

### Default Settings
`python
DEFAULT_VOICE = "es-MX-DaliaNeural"
DEFAULT_SPEED = "-10%"  # 90% of normal speed
DEFAULT_PROJECT = "mi_audio"
DEFAULT_OUTPUT = "audios_generados"
MAX_SEGMENT_LENGTH = 1000  # characters
`

### File Formats
- **Input**: UTF-8 encoded text files (.txt)
- **Output**: MP3 audio files
- **Encoding**: UTF-8 for all text processing

## Error Handling

### Common Exceptions

#### PermissionError
Occurs when output file is in use or directory is read-only.

**Handling**: Automatic filename modification with timestamp

#### ConnectionError
Network issues preventing TTS service access.

**Handling**: User notification with retry suggestion

#### FileNotFoundError
Input file not found or inaccessible.

**Handling**: Error dialog with file selection option

### Error Messages
All user-facing errors are displayed in Spanish for consistency with the target audience.

## Threading Model

### Main Thread
- GUI operations
- Event handling
- Progress updates

### Worker Thread
- Audio generation
- File I/O operations
- Network requests to TTS service

### Thread Safety
- UI updates use oot.after() for thread-safe operation
- Progress indicators updated from worker thread via callbacks

## Extension Points

### Adding New Voices
1. Add voice ID to voice selection dropdown
2. Test compatibility with Edge-TTS service
3. Update documentation

### Custom Audio Formats
1. Modify dge_tts.Communicate().save() call
2. Update file extension handling
3. Ensure media player compatibility

### Additional Languages
1. Add voice IDs for target language
2. Update UI text localization
3. Test text processing algorithms

## Performance Considerations

### Memory Usage
- Text segmentation prevents excessive memory usage
- Audio files generated sequentially
- UI remains responsive during generation

### Network Optimization
- Batch processing for multiple segments
- Retry logic for failed requests
- Progress feedback for long operations

### File I/O
- Asynchronous file operations
- Automatic directory creation
- Conflict resolution for existing files
