export type ReactionType = "like" | "dislike";

export interface ReactionRequest {
  post_id: string;
  reaction: ReactionType;
}

export interface ReactionResponse {
  success: boolean;
  message: string;
  post_id: string;
  reaction: ReactionType;
}