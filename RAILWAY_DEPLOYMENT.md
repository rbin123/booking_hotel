# Railway Deployment Configuration

# For Railway, create these files in your project root:

## railway.json (optional - for custom config)
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
  }
}

## .env.example (for environment variables)
DEBUG=False
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-railway-domain.up.railway.app

## nixpacks.toml (for Railway build configuration)
[phases.setup]
nixPkgs = ["...", "python311", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["python manage.py collectstatic --noinput"]

[start]
cmd = "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"