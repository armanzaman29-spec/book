import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';
import ErrorBoundary from '@site/src/components/ChatWidget/ErrorBoundary';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ErrorBoundary>
        <ChatWidget />
      </ErrorBoundary>
    </>
  );
}