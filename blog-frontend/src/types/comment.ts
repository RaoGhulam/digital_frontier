export interface CreateCommentPayload {
  post_id: string;
  content: string;
}

export interface CommentUser {
  id: string;
  username: string;
}

export interface CommentResponse {
  id: string;
  post_id: string;
  content: string;
  created_at: string;

  user: CommentUser;
  replies: CommentResponse[];
}