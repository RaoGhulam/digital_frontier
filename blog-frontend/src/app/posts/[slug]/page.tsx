import PostDetails from "@/components/post/PostDetails";
import { getPostBySlug } from "@/lib/api/posts";

interface Props {
  params: Promise<{
    slug: string;
  }>;
}

export default async function PostPage({ params }: Props) {
  const { slug } = await params;

  const post = await getPostBySlug(slug);

  return <PostDetails post={post} />;
}