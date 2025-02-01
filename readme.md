# 🧠 DeepSeek Chatbot with Ollama & Streamlit  

A truely local **ChatGPT-like chatbot UI** powered by **DeepSeek LLM** running locally via **Streamlit** and **Ollama**. The application provides a **real-time chat experience**, maintains conversation history, and allows users to switch between previous chats seamlessly.  

---

## **🚀 Features**  
✅ Stream responses dynamically like ChatGPT  
✅ Automatically selects the latest installed DeepSeek model based on your Mac capabillities    
✅ Saves chat history locally for future reference  
✅ Chat history tabs for switching between past conversations  
✅ Clean and intuitive UI similar to ChatGPT  

---

## **🔧 Setup & Installation**

### **Auto installation**

#### **1️⃣ Install Python Dependencies**

Install the application with few commands

* Go to the folder in which you would like to install the application
* Press **control** + **click** to open the options dropdown list 
* Select **New Terminal at Folder**
* Run the below commands

```
# Install Brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git to Clone a repo
brew install git

# Clone this GitHub repo to download and install the Chat Experience
git clone https://github.com/rahulravi-92/pocket-deepseek.git

# Navigate inside the repo
cd pocket-deepseek

# Run the below command to install the Application
chmod +x setup.sh
./setup.sh
```
---
### **Manual installation**

#### 1️⃣ Install Homebrew (If Not Installed)




```
# If installed, you’ll see the version (e.g., Homebrew 4.0.0).
brew --version

# If not installed, proceed with the installation.
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify Installation
brew --version
```

#### 2️⃣ Install Ollama

Ollama is required to run the DeepSeek model locally.

Install Ollama using this link **[https://ollama.com](https://ollama.com)**  or running the below command

```
# Install Ollama
brew install ollama

# Verify Installation
ollama --version

```

#### **3️⃣ Install Python**

```
# Check if Python is installed. If installed, you’ll see the version (e.g., Python 3.11.5).
python3 --version

# If not installed, proceed with the installation.
brew install python3

# Verify Installation
python3 --version

```
#### **4️⃣ Install Git**

```
# Check if Git is installed. If installed, you’ll see the version (e.g., git version 2.39.1).
git --version

# If not installed, proceed with the installation.
brew install git

# Verify Installation
git --version
```


#### **5️⃣ Install the application**

* Go to the folder in which you would like to install the application
* Press **control** + **click** to open the options dropdown list 
* Select **New Terminal at Folder**
* Run the below commands

```
# Download the application from the repo
git clone https://github.com/rahulravi-92/pocket-deepseek.git

# Navigate inside the folder
cd pocket-deepseek

```

#### Download the deepseek model


Pull the latest DeepSeek model using: specify a particular version, e.g.,
You can find the list [here](https://ollama.com/library/deepseek-r1)

|RAM  | Recommended Model |               Why?                                  |
| ------------- |:-------------:  |  ---------------------------------------- |
| ≥ 64GB     | deepseek-r1:67b	|  Best for high-end Macs (M3 Ultra, etc.)   |
| ≥ 32GB     | deepseek-r1:32b  |  Good for MacBook Pro (M1/M2/M3 Max) Pro      |
| ≥ 16GB     | deepseek-r1:8b   |  Optimal for MacBook Pro (M1/M2/M3)   |
| ≥ 8GB     | deepseek-r1:1.5b  |     Works, but will be slow on MacBook Air  |
| < 8GB     | ❌ Not Recommended    |   Swap-based execution will be unusable |


```
# Download the deepseek model
ollama pull deepseek-r1:8b


# Start a Virtual Environment to avoid installing lib globally
python3 -m venv .venv

# Activate the Virtual Environment
source .venv/bin/activate

# Install all the python dependencies
pip install -r requirements.txt

# And finally, run the application
streamlit run app.py

# To stop the application 
Use control + c in the terminal application

# To start again
Navigate to the Deepseek folder in finder (if not there already)
Press Control + click on the folder 
Select New Terminal at Folder

# Run application
streamlit run app.py

```



### **🔧 Uninstalling**

If you wish to remove The application and all the dependant components, follow the below steps


#### 1️⃣ Remove DeepSeek Models (Without Removing Ollama)

Run the below commands line by line.

```
# List installed models
ollama list

# Remove specific DeepSeek models
ollama rm deepseek-r1:8b

# Verify removal
ollama list
```
#### 2️⃣ Remove Ollama Completely

```
# Uninstall Ollama (if installed via Homebrew)
brew uninstall ollama

# Remove Ollama cache & configurations
rm -rf ~/.ollama
rm -rf ~/Library/Application\ Support/Ollama
rm -rf /usr/local/bin/ollama
rm -rf /opt/homebrew/bin/ollama

# Verify removal
command -v ollama || echo "Ollama successfully removed."
```

#### 3️⃣ Remove Git
```
# Check Git installation path
which git

# If installed via Homebrew:
brew uninstall git

# If installed manually, remove binaries:
sudo rm -rf /usr/local/bin/git
sudo rm -rf /usr/local/git
sudo rm -rf /etc/paths.d/git
sudo rm -rf /Library/Developer/CommandLineTools/usr/bin/git

# Verify removal
git --version || echo "Git successfully removed."
```

#### 4️⃣ Remove Python
```
# Check Python installation path
which python3

# If installed via Homebrew:
brew uninstall python3

# If installed manually:
sudo rm -rf /Library/Frameworks/Python.framework
sudo rm -rf /usr/local/bin/python3
sudo rm -rf /usr/local/lib/python3.*

# Remove Python cache & configs
rm -rf ~/.pyenv
rm -rf ~/.pip
rm -rf ~/.python_history

# Verify removal
python3 --version || echo "Python successfully removed."

```

Finally, go to the **pocket-deepseek** folder and Move it to trash.


