# Use a lightweight Python base image
FROM python:3.9-slim

# Install dependencies
RUN pip install requests

# Copy the script
COPY . .

# Run the script
CMD ["python", "update_dns.py"]
