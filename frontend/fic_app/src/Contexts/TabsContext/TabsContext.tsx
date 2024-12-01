import React, { createContext, useContext, useState, ReactNode } from "react";

export type Tab = "COMPARE" | "RECTANGLES" | "TEXT" | "STOCK";

const TabsContext = createContext<TabsContextType | undefined>(undefined);

interface TabsContextType {
    currentTab: Tab;
    setCurrentTab: React.Dispatch<React.SetStateAction<Tab>>;
}
// eslint-disable-next-line react-refresh/only-export-components
export const useTab = (): TabsContextType => {
    const context = useContext(TabsContext);
    if (!context) {
        throw new Error("useTab must be used within a PageProvider");
    }
    return context;
};

// Провайдер для контекста
export const TabsProvider = ({ children }: { children: ReactNode }) => {
    const [currentTab, setCurrentTab] = useState<Tab>("COMPARE");

    return (
        <TabsContext.Provider value={{ currentTab, setCurrentTab }}>
            {children}
        </TabsContext.Provider>
    );
};
