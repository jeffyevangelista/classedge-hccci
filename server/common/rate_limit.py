from functools import wraps
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

def custom_ratelimit(rate='5/h', method='POST', block=False, key='ip'):
    """Custom rate limit decorator with better error handling.
    
    Args:
        rate: Rate limit string (e.g., '5/h', '10/m', '100/d')
        method: HTTP methods to limit (e.g., 'POST', 'GET', 'ALL')
        block: Whether to block when limit is exceeded
        key: Key function or string ('ip', 'user', etc.)
    """
    def decorator(func):
        @wraps(func)
        @ratelimit(key=lambda group, request: get_client_ip(request), rate=rate, method=method, block=False)
        def wrapper(request, *args, **kwargs):
            # Check if rate limited
            was_limited = getattr(request, 'limited', False)
            if was_limited:
                
                # Return appropriate response based on request type
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'Rate limit exceeded. Please try again later.'
                    }, status=429)
                
                messages.error(
                    request,
                    'Too many requests. Please try again later.'
                )
                return render(
                    request,
                    'accounts/error/rate_limit.html',
                    {'retry_after': 3600},
                    status=429
                )
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
