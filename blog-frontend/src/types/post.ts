export interface Post {
  id: string;
  title: string;
  slug: string;
  category: string;
  author_name: string;
  published_at: string;
  created_at: string;

  likes: number;
  dislikes: number;
  comments: number;

  // Detail fields (optional because list API may not return them)
  content?: string;
  image?: string;
}

export interface Pagination {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface PostsResponse {
  posts: Post[];
  pagination: Pagination;
}


// Detailed Post Types

export interface PostAuthor {
  id: string;
  username: string;
}

export interface PostReactions {
  likes: number;
  dislikes: number;
}

export interface CommentUser {
  id: string;
  username: string;
}

export interface PostComment {
  id: string;
  post_id: string;
  content: string;
  created_at: string;

  user: CommentUser;
  replies: PostComment[];
}

export type ReactionType = "like" | "dislike";


export interface PostDetail {
  id: string;
  title: string;
  slug: string;
  category: string;
  content: string;

  published_at: string | null;
  created_at: string;
  updated_at: string | null;

  author: PostAuthor;

  reactions: PostReactions;
  user_reaction: ReactionType | null;

  comment_count: number;
  comments: PostComment[];
}

// Create post
export interface CreatePostPayload {
  title: string;
  slug: string;
  content: string;
  category: string;
}

export interface CreatedPost {
  id: string;
  title: string;
  slug: string;
  category: string;
  status: string;
  created_at: string;
}

export interface CreatePostResponse {
  message: string;
  post: CreatedPost;
}

export interface ApiErrorResponse {
  message: string;
}