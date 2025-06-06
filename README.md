


https://github.com/user-attachments/assets/45d1f691-c0c0-4194-a58d-f7a2debf5183



# **Node MiniMap Add-on Documentation**

**Version:** 2.9  
**Author:** ChatGPT, deepseek, duhazzz  
**For Blender:** 3.0 and above

---

## **Description**

**Node MiniMap** is a navigation tool for Blender’s **Node Editor**. It generates a compact **minimap** of all nodes in the current node tree, allowing for quick navigation and selection.

### **Key Features:**

✅ **Node Overview** – Displays all nodes in a grid layout  
✅ **Highlight Selected Nodes** – Selected nodes are marked with a smiley (😊)  
✅ **Quick Node Jump** – Click a block to center and select the corresponding node  
✅ **Popup Mode** – Open the minimap in a separate window  
✅ **Frame-Only Filter** – Show only frame nodes (useful for complex node setups)

---

## **How to Use**

### **1. Installation**

1. Download the `.py` add-on file.
    
2. In Blender, go to:  
    **Edit → Preferences → Add-ons → Install...**
    
3. Select the downloaded file and enable the add-on.
    

### **2. Accessing the Panel**

After installation, a new panel will appear in the **Node Editor**:  
**Sidebar (N) → Node MiniMap**

---

### **3. Interface & Controls**

#### **Main Controls:**

- ![Pasted image 20250606165131](https://github.com/user-attachments/assets/6c2af0a0-0429-4fba-bc7c-5b43ae14e3eb) Open in Popup** – Opens the minimap in a separate window (useful for large node trees).
    
- **☑️ Show Only Frames** – When enabled, only **frame nodes (NodeFrame)** are displayed.
    

#### **How the Minimap Works:**

- Each cell in the grid represents a node (or a group of nodes if they overlap).
    
- Node names appear if space allows.
    
- Clicking a cell **centers the view** on that node and selects it.
    
- Selected nodes are highlighted with **😊**.
    

---

## **Usage Examples**

### **🔹 Quickly Finding a Node**

1. Open the minimap (in-panel or popup).
    
2. Locate the desired node by name or position.
    
3. Click it – Blender will automatically focus on it.
    

---

**Node MiniMap makes node editing faster and smoother!** 🚀


# **Инструкция к аддону Node MiniMap**

**Версия:** 2.9  
**Автор:** ChatGPT, deepseek, duhazzz  
**Для Blender:** 3.0 и выше

---

## **Описание аддона**

**Node MiniMap** — это удобный инструмент для навигации в **Node Editor** (Редакторе узлов) Blender. Он создает миниатюрную карту (**minimap**) всех узлов в текущей нод-группе, позволяя быстро находить и переключаться между ними.

### **Основные функции:**

✅ **Миникарта узлов** — отображает все узлы в виде компактной сетки  
✅ **Подсветка выделенных узлов** — выделенные узлы помечаются смайликом (😊)  
✅ **Быстрый переход к узлу** — клик по блоку в миникарте центрирует этот узел в редакторе  
✅ **Режим попапа** — открытие миникарты в отдельном окне  
✅ **Фильтр фреймов** — отображение только узлов-фреймов (удобно для сложных нод-групп)

---

## **Как пользоваться**

### **1. Установка**

1. Скачайте файл `.py` с аддоном.
    
2. В Blender перейдите в:  
    **Edit → Preferences → Add-ons → Install...**
    
3. Выберите скачанный файл и включите аддон.
    

### **2. Где найти панель**

После установки в **Node Editor** появится новая панель:  
**Sidebar (N) → Node MiniMap**

---

### **3. Элементы управления**

#### **Основные элементы:**

- ![Pasted image 20250606165131](https://github.com/user-attachments/assets/6c2af0a0-0429-4fba-bc7c-5b43ae14e3eb) Open in Popup** 
— открывает миникарту в отдельном окне (удобно для больших нод-групп).
    
- **☑️ Show Only Frames** — если включено, миникарта показывает **только фреймы** (узлы типа _NodeFrame_).
    

#### **Как работает миникарта:**

- Каждый квадрат в сетке соответствует узлу (или группе узлов, если они близко расположены).
    
- Название узла отображается, если есть место.
    
- Клик по квадрату **перемещает вид** к этому узлу и выделяет его.
    
- Выделенные узлы помечаются смайликом **😊**.
    

---

## **Примеры использования**

### **🔹 Быстрый поиск узла**

1. Откройте миникарту в панели или попапе.
    
2. Найдите нужный узел по названию или расположению.
    
3. Кликните по нему — Blender автоматически переключится на него.
    

---

**Node MiniMap** делает работу с нодами быстрее и удобнее! 🚀
