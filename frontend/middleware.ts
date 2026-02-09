import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes that require authentication
export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/tasks'];
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // If user is accessing a protected route, we'll let the component handle authentication
  // Since localStorage is client-side only, we can't reliably check it in middleware
  // The components will handle the redirect if no token exists

  // For now, we'll allow all requests to pass through
  // Authentication will be handled in the components themselves
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};