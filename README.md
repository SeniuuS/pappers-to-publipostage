```bash
  gunicorn -w 4 -b 0.0.0.0:8686 app:gunicorn_app --daemon
  pkill gunicorn
```