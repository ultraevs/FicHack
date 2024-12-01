import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "normalize.css";
import "./index.css";
import App from "./App.tsx";
import { PageProvider } from "./Contexts/PageContext/PageContext.tsx";
import { TabsProvider } from "./Contexts/TabsContext/TabsContext.tsx";
createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <PageProvider>
            <TabsProvider>
                <App />
            </TabsProvider>
        </PageProvider>
    </StrictMode>
);
