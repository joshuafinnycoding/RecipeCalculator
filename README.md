# Recipe Calculator

A Kivy-based mobile application for managing recipes, ingredients, and calculating product pricing.

## Features

- **Ingredient Management**: Add and manage ingredients with costs
- **Product Creation**: Create products by combining ingredients
- **Recipe Scaling**: Scale recipes to different quantities
- **Pricing Calculator**: Calculate product pricing with various cost factors including:
  - Ingredient costs
  - Wastage percentage
  - Utilities and labor costs
  - Packaging and shipping
  - Taxes
  - Profit margin

## Building the APK

### Automatic Build with GitHub Actions

Push your code to GitHub and the APK will be built automatically:

1. Create a GitHub repository
2. Push this project to the repository
3. The GitHub Actions workflow will automatically build the APK
4. Download the APK from the Actions artifacts

### Manual Build

#### Requirements

- Python 3.8+
- Buildozer
- Android SDK
- Java Development Kit (JDK 17)

#### Steps

```bash
# Install dependencies
pip install buildozer cython

# Build the APK
buildozer android debug
```

The APK will be created in the `bin/` directory.

## Installation

1. Transfer the APK to your Android device
2. Enable installation from unknown sources in settings
3. Install the APK
4. Launch "Recipe Calculator" from your applications

## Development

The project uses:
- **Kivy** - UI framework
- **Python 3** - Backend logic
- **JSON** - Data storage

### Project Structure

```
RecipeCalculator/
├── main.py                 # Main application file
├── ingredients.json        # Ingredient data
├── products.json          # Product data
├── buildozer.spec         # Buildozer configuration
├── pyproject.toml         # Briefcase/project configuration
├── .github/
│   └── workflows/
│       └── build-apk.yml  # GitHub Actions workflow
└── src/
    └── recipecalculator/
        ├── __init__.py
        └── app.py         # Application code
```

## License

MIT License

## Author

Developer
