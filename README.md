# ABlog - Flask Blog Website

A modern, feature-rich blog platform built with Flask that includes user authentication, admin management, markdown support, and Progressive Web App (PWA) capabilities.

## 🚀 Features

### Core Functionality
- **User Registration & Authentication**: Secure user registration with admin approval system
- **Blog Post Management**: Create, edit, delete, and view blog posts with markdown support
- **Search Functionality**: Search posts by title, author, or tags with real-time results
- **Admin Panel**: Comprehensive admin interface for user and post management
- **Rate Limiting**: Built-in protection against abuse with Flask-Limiter
- **Responsive Design**: Mobile-first responsive design with Bootstrap 5

### Technical Features
- **Markdown Support**: Full markdown support for rich text formatting in posts
- **Dark Theme**: Elegant dark mode interface with custom styling
- **PWA Support**: Progressive Web App with service worker for offline functionality
- **Database Management**: SQLite database with automatic yearly partitioning for posts
- **Session Management**: Secure session handling with Flask sessions
- **Pagination**: Efficient post loading with pagination support

### Security Features
- **Password Hashing**: Secure SHA-256 password hashing
- **Rate Limiting**: Protection against brute force attacks and spam
- **Session Security**: Secure session management
- **Admin Approval**: User registration requires admin approval
- **Input Validation**: Server-side validation for all user inputs

## 📁 Project Structure

```
Blog-Website/
├── app.py                 # Main application entry point
├── routes.py              # Flask routes and endpoint definitions
├── methods.py             # Database models and business logic
├── requirements.txt       # Python dependencies
├── service-worker.js      # PWA service worker
├── static/
│   ├── bootstrap/         # Bootstrap CSS and JS files
│   ├── styles.css         # Custom dark theme styles
│   ├── scripts.js         # Frontend JavaScript functionality
│   ├── offline.html       # PWA offline page
│   └── POSTS/            # SQLite databases for posts (yearly)
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Homepage with post listing
│   ├── login_registration.html # User authentication page
│   ├── create_post.html   # Post creation/editing interface
│   ├── admin.html         # Admin panel interface
│   ├── profile.html       # User dashboard
│   ├── about.html         # About page
│   └── post.html          # Individual post view
├── access.log             # Access logs
├── error.log              # Error logs
└── User.db               # Main user database
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashupal86/Blog-Website
   cd Blog-Website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   The application will automatically create the necessary SQLite databases on first run.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 📋 Dependencies

The project uses the following main dependencies:

- **Flask 3.1.0**: Web framework
- **Flask-Limiter 3.9.2**: Rate limiting
- **mistune 3.0.2**: Markdown processing
- **waitress 3.0.2**: WSGI server for production
- **Pygments 2.18.0**: Syntax highlighting
- **pymemcache 4.0.0**: Memcached client for rate limiting
- **Bootstrap 5**: Frontend framework (included in static files)

For a complete list of dependencies, see `requirements.txt`.

## 🎯 Usage

### For Users

1. **Registration**: Submit a registration request with username, password, email, age, and phone number
2. **Approval**: Wait for admin approval to activate your account
3. **Login**: Use your credentials to access the platform
4. **Create Posts**: Write blog posts using markdown syntax
5. **Search**: Use the search bar to find posts by title, author, or tags
6. **Profile**: Manage your posts from your profile dashboard

### For Administrators

1. **Admin Login**: Access the admin panel at `/admin_login`
2. **User Management**: 
   - Approve or deny pending registrations
   - Delete existing users
   - Add new administrators
3. **Content Management**: 
   - View and manage all posts
   - Restore deleted posts
   - Monitor user activity

## 🔧 Configuration

### Database Configuration
- **User Database**: `User.db` - Stores user accounts and admin data
- **Posts Database**: `static/POSTS/Post_YYYY.db` - Posts are stored in yearly databases
- **Automatic Setup**: Databases are created automatically on first run

### Rate Limiting
The application includes rate limiting on sensitive endpoints:
- Login attempts: 5 per minute
- Registration: 2 per minute
- Post creation: 1 per minute
- Default routes: 10 per minute

### Admin Configuration
- A default admin account is created automatically
- Admin credentials are stored securely in the database
- Admins can create additional admin accounts

## 🎨 Customization

### Styling
- **Dark Theme**: The application uses a custom dark theme defined in `static/styles.css`
- **Responsive Design**: Bootstrap 5 ensures mobile compatibility
- **Custom Fonts**: Uses Google Fonts (Lora and Open Sans)

### Markdown Support
Posts support full markdown syntax including:
- Headers (H1-H6)
- Bold, italic, and strikethrough text
- Ordered and unordered lists
- Links and images
- Code blocks with syntax highlighting
- Blockquotes and horizontal rules

## 🚀 Production Deployment

The application is configured for production deployment:

1. **WSGI Server**: Uses Waitress as the WSGI server
2. **Logging**: Comprehensive logging to `access.log` and `error.log`
3. **Security**: Production-ready security configurations
4. **Performance**: Optimized database queries and caching

### Production Run
```bash
python app.py
```
The application will serve on `0.0.0.0:8000` by default.

## 📱 Progressive Web App (PWA)

The application includes PWA features:
- **Service Worker**: Enables offline functionality
- **Responsive Design**: Works seamlessly on mobile devices
- **Installable**: Can be installed as a native app on supported devices
- **Offline Support**: Basic offline functionality with cached content

## 🔒 Security Features

- **Password Security**: SHA-256 password hashing
- **Session Management**: Secure Flask sessions
- **Rate Limiting**: Protection against abuse and attacks
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Parameterized queries throughout
- **XSS Protection**: Template escaping and input sanitization

## 🐛 Error Handling

The application includes comprehensive error handling:
- **Database Errors**: Graceful handling of SQLite errors
- **Rate Limiting**: 429 error pages for rate limit violations
- **User Feedback**: Flash messages for user actions
- **Logging**: Detailed error logging for debugging

## 📊 Logging & Monitoring

- **Access Logs**: HTTP request logging in `access.log`
- **Error Logs**: Application error logging in `error.log`
- **Activity Logs**: User activity tracking in `log.txt`
- **Admin Actions**: Audit trail for admin activities

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support or questions:
1. Check the error logs for debugging information
2. Review the code documentation in the source files
3. Ensure all dependencies are properly installed
4. Verify database permissions and file access

## 🔮 Future Enhancements

Potential areas for enhancement:
- Email notifications for registration approval
- Image upload functionality for posts
- Comment system for posts
- Social media integration
- Advanced search filters
- User profile customization
- Post categories and tags management
- RSS feed generation
- API endpoints for mobile app integration 