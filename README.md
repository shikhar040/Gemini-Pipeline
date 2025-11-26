# 🤖 AI Auto-Healing Pipeline

An intelligent auto-healing pipeline powered by Gemini AI that automatically fixes project structure, file names, and deployment issues.

## 🚀 Features

- **AI-Powered Healing**: Uses Gemini AI to analyze and fix project issues
- **Automatic Deployment**: Deploys to Netlify via GitHub Actions
- **Smart File Renaming**: Fixes problematic file names and extensions
- **Project Structure Optimization**: Organizes files for optimal web deployment

Excellent! 🎉 Now that your auto-healer is working, here are some **test cases** to verify it's working properly:

## 🧪 **TEST CASES FOR AUTO-HEALER**

### **Test Case 1: File Extension Fixes**
```bash
# Create files with wrong extensions
echo "JS content" > "public/wrong-extension.jx"
echo "HTML content" > "public/page.htm"
echo "Python script" > "src/script.PY"
echo "CSS content" > "public/style.cssx"
```

**Expected Result:**
- `wrong-extension.jx` → `wrong-extension.js`
- `page.htm` → `page.html` 
- `script.PY` → `script.py`
- `style.cssx` → `style.css`

### **Test Case 2: Spaces and Special Characters**
```bash
# Create files with spaces and special chars
echo "Content" > "public/file with spaces.js"
echo "Content" > "public/bad@file#name.html"
echo "Content" > "src/my test file.py"
echo "Content" > "public/User Profile Page.htm"
```

**Expected Result:**
- `file with spaces.js` → `file-with-spaces.js`
- `bad@file#name.html` → `bad-file-name.html`
- `my test file.py` → `my-test-file.py`
- `User Profile Page.htm` → `user-profile-page.html`

### **Test Case 3: Case Sensitivity**
```bash
# Create files with uppercase
echo "Content" > "public/MyPage.HTML"
echo "Content" > "src/MainScript.JS"
echo "Content" > "public/Config.File.JSON"
```

**Expected Result:**
- `MyPage.HTML` → `mypage.html`
- `MainScript.JS` → `mainscript.js`
- `Config.File.JSON` → `config.file.json`

### **Test Case 4: Index File Scenarios**
```bash
# Test index file variations
echo "Home page" > "public/index.htm"
echo "Alt home" > "public/INDEX.HTM"
echo "Main page" > "index.htm"  # In root directory
```

**Expected Result:**
- All should become `index.html` in `public/` folder

### **Test Case 5: Mixed Issues**
```bash
# Files with multiple problems
echo "Content" > "public/My @Page With Spaces.jx"
echo "Content" > "src/TEST File.PY"
echo "Content" > "public/home page.HTM"
```

**Expected Result:**
- `My @Page With Spaces.jx` → `my-page-with-spaces.js`
- `TEST File.PY` → `test-file.py`
- `home page.HTM` → `home-page.html`

## 🚀 **QUICK TEST SCRIPT**

Create a test script to run all cases at once:

**`tests/run-tests.sh`**
```bash
#!/bin/bash
echo "🧪 RUNNING AUTO-HEALER TEST CASES"

# Test Case 1: Wrong extensions
echo "1. Testing wrong extensions..."
echo "JS content" > "public/wrong-extension.jx"
echo "HTML content" > "public/page.htm"

# Test Case 2: Spaces and special chars  
echo "2. Testing spaces and special chars..."
echo "Content" > "public/file with spaces.js"
echo "Content" > "public/bad@file#name.html"

# Test Case 3: Uppercase files
echo "3. Testing uppercase files..."
echo "Content" > "public/MyPage.HTML"

echo "✅ Test files created. Push to trigger auto-healer!"
```

## 📊 **VERIFICATION CHECKLIST**

After pushing test files, check:

### **In GitHub Actions Logs:**
- ✅ "FILES BEFORE HEALING" shows your bad files
- ✅ "RUNNING SIMPLE AUTO-HEALER" shows fixes being applied
- ✅ "FILES AFTER HEALING" shows corrected files
- ✅ "AUTO-HEAL: Fix file names" commit appears

### **In Your Repository:**
- ✅ All files have correct extensions (.js, .html, .py)
- ✅ No spaces in filenames (uses hyphens)
- ✅ No special characters (@, #, $, etc.)
- ✅ All lowercase (except where appropriate)
- ✅ `public/index.html` exists and is correct

## 🔍 **MANUAL VERIFICATION COMMANDS**

After auto-healer runs, check with:
```bash
# Check what files exist now
find . -name "*.js" -o -name "*.html" -o -name "*.py" | sort

# Check if any problematic files remain
find . -name "* *" -o -name "*.jx" -o -name "*.htm" -o -name "*.PY"
```

## 🎯 **EDGE CASE TESTS**

### **Test Edge Cases:**
```bash
# Files that should NOT be changed
echo "README" > "README.md"  # Should stay .md
echo "Config" > ".gitignore" # Should stay .gitignore
echo "Data" > "data.JSON"    # Should become data.json
echo "Note" > "NOTE.txt"     # Should become note.txt
```

### **Nested Directory Test:**
```bash
# Test files in nested directories
mkdir -p "src/components/my component"
echo "React code" > "src/components/my component/Button.jx"
echo "Styles" > "src/components/my component/Style.cssx"
```

## 📝 **TEST REPORT TEMPLATE**

Create a test report file:

**`test-results.md`**
```markdown
# Auto-Healer Test Results

## Test Date: [Date]

### ✅ Fixed Successfully:
- [ ] wrong-extension.jx → wrong-extension.js
- [ ] file with spaces.js → file-with-spaces.js  
- [ ] MyPage.HTML → mypage.html

### ❌ Issues Found:
- [ ] Any files not fixed?

### 🔧 Auto-Healer Performance:
- Fixes applied: [number]
- Time taken: [duration]
- Success rate: [percentage]
```

## 🚀 **RUN A COMPREHENSIVE TEST**

```bash
# Create all test cases at once
mkdir -p tests
./tests/run-tests.sh

# Commit and push to trigger auto-healer
git add .
git commit -m "TEST: Comprehensive auto-healer test cases"
git push
```

**Run these test cases and your auto-healer should handle them all perfectly!** Let me know which ones work and if you find any edge cases it misses. 🧪🚀
