class AppError(Exception):
    """
    Base application exception.

    All business/service layer exceptions should inherit from this class.
    """

    status_code = 400
    message = "Application error"


# =========================
# Authentication / Users
# =========================

class AuthenticationError(AppError):
    status_code = 401
    message = "Invalid credentials"

class InvalidTokenError(AuthenticationError):
    status_code = 401
    message = "Invalid token"

class InvalidCredentialsError(AuthenticationError):
    status_code = 401
    message = "Invalid credentials"

class UserNotFoundError(AuthenticationError):
    status_code = 401
    message = "User not found"

class UserDeletedError(AuthenticationError):
    status_code = 401
    message = "User account is deleted"

class UserAlreadyExistsError(AppError):
    status_code = 409
    message = "User already exists"

class UserInactiveError(AppError):
    status_code = 403
    message = "User account is inactive"

class LoginRateLimitExceededError(AppError):
    status_code = 429
    message = "Too many login attempts. Please try again later."

class EmailVerificationTokenInvalid(AppError):
    status_code = 401
    message = "Email verification token is invalid or expired"

class EmailNotVerifiedError(AppError):
    status_code = 403
    message = "Please verify your email before logging in."


# =========================
# Admin
# =========================

class AdminAuthError(AppError):
    status_code = 401
    message = "Admin authentication failed"


class AdminNotFoundError(AdminAuthError):
    status_code = 404
    message = "Admin not found"


class AdminInactiveError(AdminAuthError):
    status_code = 403
    message = "Admin account is inactive"


class AdminPermissionError(AppError):
    status_code = 403
    message = "Permission denied"

class SuperAdminRequiredError(AppError):
    status_code = 403
    message = "Superadmin access required"
    
# =========================
# Post Moderation
# =========================

class PostModerationError(AppError):
    status_code = 400
    message = "Post moderation error"


class PendingPostNotFoundError(PostModerationError):
    status_code = 404
    message = "Pending post not found"


class InvalidModerationActionError(PostModerationError):
    status_code = 400
    message = "Invalid moderation action"


# =========================
# Posts
# =========================

class PostException(AppError):
    status_code = 400
    message = "Post error"


class PostNotFoundError(PostException):
    status_code = 404
    message = "Post not found"


class PermissionDenied(PostException):
    status_code = 403
    message = "Permission denied"


class DuplicateSlugError(PostException):
    status_code = 409
    message = "Post slug already exists"


class DatabaseError(PostException):
    """
    Internal database failure.

    Do not expose database details to clients.
    """

    status_code = 500
    message = "Unable to process request"


# =========================
# Comments
# =========================

class CommentNotFoundError(AppError):
    status_code = 404
    message = "Comment not found"


class CommentPermissionError(AppError):
    status_code = 403
    message = "Permission denied"


# =========================
# Reactions
# =========================

class ReactionNotFoundError(AppError):
    status_code = 404
    message = "Reaction not found"