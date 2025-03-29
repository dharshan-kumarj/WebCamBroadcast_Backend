from django.http import JsonResponse
from django.shortcuts import render
import uuid

def get_stream_id(request):
    """Generate a unique stream ID for a broadcaster"""
    stream_id = str(uuid.uuid4())[:8]
    return JsonResponse({'stream_id': stream_id})

def broadcaster_page(request):
    """Render the broadcaster interface"""
    return render(request, 'broadcast_app/broadcaster.html')

def viewer_page(request, stream_id):
    """Render the viewer interface"""
    return render(request, 'broadcast_app/viewer.html', {'stream_id': stream_id})