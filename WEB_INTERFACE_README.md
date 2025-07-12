# AutoInvestigator Web Interface

A modern, immersive web interface for the AutoInvestigator AI-powered financial analysis platform. Built with Flask, featuring stunning animations and interactive elements inspired by Perplexity AI's design.

## 🌟 Features

### Landing Page

- **Immersive Animations**: Floating gradient orbs, particle effects, and smooth transitions
- **Modern Design**: Dark theme with glassmorphism effects and gradient accents
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Interactive Elements**: Hover effects, scroll animations, and smooth navigation
- **Typewriter Effects**: Animated text reveals for engaging user experience

### Investigation Interface

- **Chat-like Design**: Modern conversation interface similar to Perplexity AI
- **Real-time Interaction**: Instant message sending and response display
- **Tool Selection**: Choose from different investigation tools (Financial, News, SEC, Sentiment, Risk)
- **Results Panel**: Dedicated area for displaying investigation results
- **Loading Animations**: Beautiful loading states with step-by-step progress
- **Auto-resize Input**: Dynamic textarea that grows with content

### Technical Features

- **Flask Backend**: Python-based web server with RESTful API
- **Modern CSS**: CSS Grid, Flexbox, and advanced animations
- **JavaScript ES6+**: Modern JavaScript with classes and async/await
- **Responsive Design**: Mobile-first approach with breakpoints
- **Performance Optimized**: Efficient animations and lazy loading

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd autoinvestigator
   ```

2. **Run the web application launcher**

   ```bash
   python run_web_app.py
   ```

3. **Access the application**
   - Landing page: http://localhost:5000
   - Investigation interface: http://localhost:5000/investigate

The launcher will automatically:

- Check and install required dependencies
- Set up the environment
- Start the Flask server
- Open your default browser

## 📁 Project Structure

```
client/
├── web_app.py              # Flask application
├── templates/
│   ├── landing.html        # Landing page template
│   └── investigate.html    # Investigation interface template
├── static/
│   ├── css/
│   │   ├── landing.css     # Landing page styles
│   │   └── investigate.css # Investigation interface styles
│   └── js/
│       ├── landing.js      # Landing page interactions
│       └── investigate.js  # Investigation interface logic
└── agent.py               # AI agent integration

run_web_app.py             # Application launcher
```

## 🎨 Design Features

### Color Scheme

- **Primary**: Purple gradient (#667eea to #764ba2)
- **Secondary**: Blue gradient (#4facfe to #00f2fe)
- **Accent**: Pink gradient (#f093fb to #f5576c)
- **Background**: Dark theme (#0a0a0a to #16213e)

### Animations

- **Floating Orbs**: Continuous gradient orbs with rotation
- **Particle Effects**: Subtle background particles
- **Scroll Animations**: Elements animate as they enter viewport
- **Hover Effects**: Interactive feedback on buttons and cards
- **Loading States**: Multi-ring spinner with step animations

### Typography

- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Hierarchy**: Clear visual hierarchy with proper spacing

## 🔧 Customization

### Modifying Colors

Edit the CSS variables in the respective CSS files:

```css
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --background: #0a0a0a;
}
```

### Adding New Tools

1. Add tool item to `investigate.html`:

   ```html
   <div class="tool-item" data-tool="new-tool">
     <i class="fas fa-icon"></i>
     <span>New Tool</span>
   </div>
   ```

2. Handle in `investigate.js`:
   ```javascript
   // Add tool-specific logic in the investigate method
   ```

### Styling Modifications

- **Landing Page**: Edit `client/static/css/landing.css`
- **Investigation Interface**: Edit `client/static/css/investigate.css`
- **Animations**: Modify keyframes and transition properties

## 🌐 Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### Known Issues

- Safari: Some backdrop-filter effects may not render properly
- Mobile: Touch interactions optimized for modern mobile browsers

## 🔌 API Integration

The web interface communicates with the backend through RESTful APIs:

### Investigation Endpoint

```
POST /api/investigate
Content-Type: application/json

{
  "query": "Analyze Apple's financial performance",
  "tool": "all"
}
```

### Response Format

```json
{
  "status": "success",
  "message": "Investigation completed for: Apple",
  "results": {
    "financial": "Financial analysis shows...",
    "news": "Recent news sentiment...",
    "sentiment": "Sentiment analysis reveals...",
    "risk": "Risk assessment shows..."
  },
  "tool_used": "all",
  "timestamp": 1640995200
}
```

## 🚀 Deployment

### Local Development

```bash
python run_web_app.py
```

### Production Deployment

1. Set environment variables:

   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 client.web_app:app
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run_web_app.py"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**

   ```bash
   # Find and kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Dependencies not found**

   ```bash
   pip install flask flask-cors
   ```

3. **Import errors**

   - Ensure you're running from the project root
   - Check Python path includes the project directory

4. **Static files not loading**
   - Verify file paths in templates
   - Check Flask static folder configuration

### Debug Mode

Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python run_web_app.py
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use consistent indentation (2 spaces for CSS, 4 for Python)
- Add comments for complex logic
- Keep functions small and focused

## 📄 License

This project is part of the AutoInvestigator platform. See the main project license for details.

## 🤝 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the main project documentation
3. Open an issue on the project repository

---

**Built with ❤️ using Flask, modern CSS, and JavaScript**
