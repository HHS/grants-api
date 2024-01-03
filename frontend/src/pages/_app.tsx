import { GoogleTagManager } from "@next/third-parties/google";
import { PUBLIC_ENV } from "src/constants/environments";

import { appWithTranslation } from "next-i18next";
import type { AppProps } from "next/app";
import Head from "next/head";

import Layout from "../components/Layout";

import "../styles/styles.scss";

import { assetPath } from "src/utils/assetPath";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <link rel="icon" href={assetPath("/img/favicon.ico")} sizes="any" />
      </Head>
      <GoogleTagManager gtmId={PUBLIC_ENV.GOOGLE_TAG_ID} />
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </>
  );
}

export default appWithTranslation(MyApp);
