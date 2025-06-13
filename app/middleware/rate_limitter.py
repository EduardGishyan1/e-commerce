import time
from collections import defaultdict
from typing import Dict

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.settings import settings

class AdvancedMiddleware(BaseHTTPMiddleware):
  def __init__(self, app):
    super().__init__(app)
    self.rate_limit_records: Dict[str, list] = defaultdict(list)
    self.max_requests = settings.MAX_REQUESTS_PER_MINUTE
    self.time_limit = settings.REQUESTS_TIME_LIMIT

  async def dispatch(self, request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    self.rate_limit_records[client_ip] = [
      t for t in self.rate_limit_records[client_ip] if current_time - t < self.time_limit]

    if len(self.rate_limit_records[client_ip]) >= self.max_requests:
      return JSONResponse(content="Rate limit exceeded. Try again in 1 minute.", status_code=status.HTTP_429_TOO_MANY_REQUESTS)

    self.rate_limit_records[client_ip].append(current_time)

    response = await call_next(request)
    return response