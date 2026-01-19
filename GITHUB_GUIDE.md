# Beginner's Guide: How to Get Your APK via GitHub

Don't worry if you haven't used GitHub before! It's just a place to store code, and I've set up a "robot" (called GitHub Actions) that will build your APK automatically once the code is there.

Follow these exact steps:

### 1. Create a GitHub Account
- Go to [github.com](https://github.com/) and sign up for a free account.

### 2. Create a "Repository" (A folder for your code)
- On your GitHub home page, look for a green button that says **"New"** (next to "Repositories").
- Give it a name, for example: `smp-mobile-app`.
- Keep it "Public" (it's easier for the robot to work).
- Click **"Create repository"** at the bottom.

### 3. Upload Your Files
- On the next screen, you will see a link that says **"uploading an existing file"**. Click that.
- Select **ALL** the files from your `c:\Users\mehmo\Documents\Python` folder (including the `.github` folder I created).
    - *Tip: You can just drag and drop them into the browser.*
- Scroll down and click the green **"Commit changes"** button.

### 4. Wait for the Robot to Build Your APK
- Click the **"Actions"** tab at the top of your repository page.
- You will see a task named **"Build Android APK"**. It might have a yellow circling icon (this means it's working).
- Wait about 5-8 minutes until it turns into a green checkmark ✅.

### 5. Download and Install
- Click on that "Build Android APK" task.
- Scroll down to the bottom where it says **"Artifacts"**.
- Click on **"smp-extraction-apk"**. It will download as a `.zip` file.
- Unzip it, and you'll find the `.apk` file inside!
- Send that `.apk` to your phone and install it.

> [!TIP]
> **Can't find the .github folder?**
> Windows sometimes hides folders starting with a dot. If you don't see it, I have placed it exactly where your other python files are. Ensure you select "Show hidden files" in your Windows folder settings.

---

### Alternative: Use the app on your phone WITHOUT an APK
If the above feels too complicated, you can use an app called **Pydroid 3** from the Play Store. 
1. Install **Pydroid 3**.
2. Copy your python files to your phone.
3. Open `gui.py` in Pydroid 3 and press Play!
