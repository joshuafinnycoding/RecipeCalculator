# GitHub Setup Instructions

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in (or create an account)
2. Click the **"+"** icon in the top right and select **"New repository"**
3. Name your repository: `RecipeCalculator`
4. Choose visibility: Public (for GitHub Actions to work) or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Add Remote and Push Code

After creating the repository, you'll see commands. Run these in your terminal:

```bash
cd c:\Users\joshua.finny\RecipeCalculator

# Add the remote repository (replace YOUR_USERNAME and your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/RecipeCalculator.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Step 3: Watch GitHub Actions Build

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see the "Build APK" workflow running
4. Wait for it to complete (usually 5-10 minutes)
5. Once complete, click on the workflow run
6. Scroll down to **"Artifacts"** section
7. Download the `recipe-calculator-apk` artifact containing your APK!

## Step 4: Install on Android Device

1. Transfer the APK to your Android device via:
   - USB cable + file transfer
   - Email
   - Cloud storage (Google Drive, OneDrive, etc.)
   - QR code from a file transfer service

2. On your Android device:
   - Open Settings → Security
   - Enable "Unknown Sources" or "Install from Unknown Sources"
   - Find the APK file using a file manager
   - Tap to install
   - Launch "Recipe Calculator" from your apps

## What the Workflow Does

The GitHub Actions workflow (`.github/workflows/build-apk.yml`):

✅ Sets up Java 17 JDK
✅ Sets up Android SDK
✅ Installs Python dependencies
✅ Builds the APK with Buildozer
✅ Uploads the APK as an artifact
✅ Creates releases when you tag commits

## Tips

- **Update the app**: Push changes to the `main` branch, and the APK rebuilds automatically
- **Create releases**: Tag commits with `git tag v1.0.0` and push with `git push --tags` to create official releases
- **Share the APK**: Download from artifacts and share with others

## Troubleshooting

If the build fails:
1. Check the workflow logs in the **"Actions"** tab
2. Common issues: Missing permissions, outdated buildozer.spec
3. You can view detailed logs by clicking on the failed workflow run

## Next Steps

Once you have the APK:
1. Test it on your Android device
2. Make improvements to the app
3. Push updates to GitHub - the APK rebuilds automatically!
