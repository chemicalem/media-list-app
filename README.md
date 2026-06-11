# PR Pulse - Smart Media Query Explorer & AI Pitching Assistant

A powerful, intelligent platform for PR professionals to discover media opportunities, analyze target outlets, and generate personalized pitch responses using Google Gemini AI.

## 🌟 Features

- **📊 Media Query Management**: Import and organize media queries from CSV files
- **🔍 Advanced Filtering**: Filter by category, Domain Authority (DA), journalist name, and outlet
- **🤖 AI-Powered Search**: Semantic search expansion using Gemini for better query matching
- **🎯 Smart Matchmaking**: AI analyzes your expert profile against media opportunities to find perfect fits
- **✍️ Auto-Generated Pitches**: Gemini drafts targeted PR responses based on journalist questions
- **💾 Export Results**: Download filtered opportunities and AI-matched reports as CSV
- **⚡ Real-time Analytics**: Dashboard with matching queries, average DA, and active deadline counts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key ([Get one free](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chemicalem/media-list-app.git
   cd media-list-app
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

**Option 1: Streamlit (Python)**
```bash
streamlit run main.py
```
The app will open at `http://localhost:8501`

**Option 2: HTML Version**
Open `index.html` directly in your browser (no server needed)

## 📋 CSV Format

Your media queries CSV should include these columns:
```
SUMMARY, CATEGORY, QUERY, QUESTIONS, MEDIA_OUTLET, DA, NAME, EMAIL, DEADLINE_DATE
```

### Example Row
```
"How Fintech is Changing Consumer Habits","Business and Finance","Seeking fintech experts...","What consumer behaviors changed most?","Techcabal","82","Innes Wong","inneswong8@gmail.com","2026-06-21"
```

Supported column name variations:
- `SUMMARY` | `TITLE`
- `CATEGORY` | `TOPIC`
- `NAME` | `REPORTER` | `JOURNALIST`
- `MEDIA OUTLET` | `OUTLET` | `SOURCE`
- `DA` | `DOMAIN AUTHORITY`
- `QUERY` | `DESCRIPTION`

## 🔧 Configuration

### Setting Your Expert Profile
1. Save your professional background in the sidebar
2. Include credentials, expertise, and unique value proposition
3. Gemini uses this to find matching opportunities and draft personalized pitches

### Adding Gemini API Key
1. Get your free API key at [https://ai.google.dev/](https://ai.google.dev/)
2. Enter it in the app sidebar under "Gemini API Setup"
3. Key is used only for current session (not saved)

## 💡 How to Use

### Workflow
1. **Import Data**: Upload CSV or load sample data
2. **Refine Search**: Use filters on left sidebar to narrow results
3. **Find Matches**: Run AI Matchmaker to score opportunities
4. **Draft Pitches**: Open any opportunity and click "Draft AI Pitch"
5. **Export**: Download results and AI reports

### Smart Search Brain
- Type vague product concepts
- Gemini expands into semantic keywords
- Auto-matches against loaded media queries
- Shows AI reasoning for transparency

### AI Matchmaker
- Analyzes top 10 filtered opportunities
- Scores fit percentage (0-100)
- Provides AI reasoning for each match
- Export results to CSV

## 📁 Project Structure

```
media-list-app/
├── main.py              # Streamlit application (Python)
├── index.html           # Standalone HTML version
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## 🛠 Technologies

- **Frontend**: Streamlit (Python) or vanilla HTML/Tailwind CSS
- **AI Engine**: Google Gemini 2.5 Flash
- **Data Processing**: Pandas, PapaParse (CSV)
- **Styling**: Tailwind CSS, Streamlit native components

## 📊 Supported Filters

- **Category**: Filter by topic (Finance, Tech, Lifestyle, etc.)
- **Domain Authority**: Minimum DA threshold (0-100)
- **Journalist Name**: Search by reporter
- **Media Outlet**: Search by publication
- **Deadline Status**: Include/exclude passed deadlines

## 🔐 Privacy & Security

- ✅ No data stored on servers
- ✅ CSV uploads processed locally only
- ✅ Expert bio never leaves browser/session
- ✅ Gemini API calls encrypted in transit
- ✅ Each session is completely isolated

## 📝 Sample Data

Load demo PR opportunities with the "Load Sample Data" button:
- Fintech innovations (Techcabal)
- Puerto Rican rum history (Mitu)
- Engineering burnout (Wired Tech)

## 🐛 Troubleshooting

**"No Gemini API key found"**
- Add your API key in the sidebar under "Gemini API Setup"
- Free keys available at [https://ai.google.dev/](https://ai.google.dev/)

**"CSV parsing failed"**
- Ensure column names match expected format
- Check for UTF-8 encoding (not Excel native format)
- Try opening in Google Sheets and re-exporting

**"AI response was empty"**
- Check your Gemini API quota/rate limits
- Verify API key is valid
- Try again in a few moments

## 🚀 Deployment

### Streamlit Cloud
```bash
git push origin main
# Then connect repo at https://streamlit.io/cloud
```

### Self-hosted
```bash
streamlit run main.py --server.port 8000 --server.address 0.0.0.0
```

## 📞 Support

For issues or feature requests, open a GitHub issue.

## 📄 License

MIT License - feel free to use and modify

---

**Built with ⚡ for PR professionals who want smarter media outreach**