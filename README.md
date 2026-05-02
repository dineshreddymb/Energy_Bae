# Energy Bae - Solar Calculator

## 🌞 Project Overview

**Energy Bae** is an intelligent solar energy recommendation system that analyzes electricity bills and provides personalized solar installation recommendations. The application uses AI-powered document processing to extract billing information and calculate optimal solar capacity for residential and commercial customers.

## ✨ Features

- **📄 Bill Upload**: Upload electricity bills as PDF or image files (PNG, JPG, JPEG)
- **🤖 AI-Powered Analysis**: Uses Groq API to extract and analyze bill data
- **☀️ Solar Recommendations**: Calculates required solar capacity (kW) and number of panels
- **📊 Comprehensive Metrics**: Displays monthly units, tariffs, billing period, and consumption levels
- **💰 Savings Prediction**: Estimates bill reduction with solar installation
- **📈 Detailed Reports**: Downloadable Excel reports with complete analysis
- **⚡ Real-time Processing**: N8N webhook integration for fast, reliable processing

## 🛠 Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend Workflow**: N8N (automation platform)
- **AI Engine**: Groq API (large language model)
- **Document Processing**: PIL (image handling)
- **API Communication**: Requests library
- **Data Export**: OpenPyXL (Excel generation)

## 📋 Prerequisites

- Python 3.8+
- Streamlit
- N8N instance with configured webhook
- Groq API key
- Required Python packages (see requirements.txt)

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/dineshreddymb/Energy_Bae.git
cd Energy_Bae
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
Create a `.env` file with:
```
N8N_WEBHOOK_URL=your_n8n_webhook_url
API_KEY=your_api_key
GROQ_API_KEY=your_groq_api_key
```

## 💻 Usage

1. **Start the Streamlit app**:
```bash
streamlit run app.py
```

2. **Upload an electricity bill**:
   - Click "Upload Electricity Bill"
   - Select a PDF or image file of your electricity bill

3. **Get recommendations**:
   - Click "Calculate Solar Recommendation"
   - View instant analysis and solar capacity recommendations

4. **Download report**:
   - Click "Download Excel Report" to get detailed recommendations

## 📊 Extracted Data

The app extracts and displays:
- Customer name and consumer number
- Monthly units consumed
- Total bill amount and unit cost
- Billing period and tariff category
- Sanctioned load (connection capacity)
- Daily average consumption
- Recommended solar capacity (kW)
- Recommended number of solar panels
- Predicted savings on next month's bill

## 🔧 API Workflow

The application follows this workflow:
1. User uploads electricity bill
2. Streamlit sends file to N8N webhook
3. N8N processes file with Groq AI
4. AI extracts bill details in JSON format
5. Results returned to Streamlit frontend
6. User views analysis and recommendations

## 📦 Dependencies

See `requirements.txt` for complete list:
- streamlit==1.28.0
- requests==2.31.0
- pandas==2.1.0
- openpyxl==3.1.2
- Pillow==10.0.1
- python-dotenv==1.0.0

## ⚠️ Important Notes

- **.env file**: Never commit `.env` file with API keys to version control
- **Webhook Configuration**: Ensure N8N webhook URL is correctly set
- **API Quotas**: Monitor Groq API usage to avoid exceeding quotas
- **File Formats**: Supported formats are PDF and common image formats

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing N8N_WEBHOOK_URL" | Add webhook URL to .env file |
| "GROQ API Missing" | Get API key from Groq and add to .env |
| Bill processing timeout | Increase timeout value or check n8n workflow status |
| Invalid JSON response | Ensure bill format is clear and readable |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Dinesh Reddy**  
GitHub: [@dineshreddymb](https://github.com/dineshreddymb)

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Last Updated**: May 2, 2026  
**Version**: 1.0.0