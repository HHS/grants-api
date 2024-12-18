/**
 * Configure the UserProvider component.
 *
 * If you have any server-side rendered pages (using `getServerSideProps` or Server Components), you should get the
 * user from the server-side session and pass it to the `<UserProvider>` component via the `user`
 * prop. This will prefill the useUser hook with the UserProfile object.
 * For example:
 *
 * import { UserProvider } from 'src/services/auth/UserProvider';
 *
 * export default async function RootLayout({ children }) {
 *   // this will emit a warning because Server Components cannot write to cookies
 *   // see https://github.com/auth0/nextjs-auth0#using-this-sdk-with-react-server-components
 *   const session = await getSession();
 *
 *   return (
 *     <html lang="en">
 *       <body>
 *         <UserProvider user={session?.user}>
 *           {children}
 *         </UserProvider>
 *       </body>
 *     </html>
 *   );
 * }
 * ```
 *
 * In client-side rendered pages, the useUser hook uses a UserFetcher to fetch the
 * user from the profile API route. If needed, you can specify a custom fetcher here in the
 * `fetcher` option.
 *
 *
 * @category Client
 */

/**
 * The user claims returned from the useUser hook.
 *
 * @category Client
 */
export interface UserProfile {
  name?: string | null;
}

export type UserSession = {
  token: string;
  expiresAt?: Date;
} | null;

export type SessionPayload = {
  token: string;
  expiresAt: Date;
};

/**
 * Fetches the user from the profile API route to fill the useUser hook with the
 * UserProfile object.

 */
export type UserFetcher = (url: string) => Promise<SessionPayload | undefined>;

/**
 * @ignore
 */
export type UserProviderState = {
  user?: UserSession;
  error?: Error;
  isLoading: boolean;
};
