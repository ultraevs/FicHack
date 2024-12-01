import React, { createContext, useContext, useState, ReactNode } from "react";

export type Page =
    | "MAIN"
    | "INTERFACE"
    | "PHOTOS"
    | "HISTORY"
    | "LOGIN"
    | "LOGOUT"
    | "REGISTER";

interface PageContextType {
    currentPage: Page;
    setCurrentPage: React.Dispatch<React.SetStateAction<Page>>;
}
const PageContext = createContext<PageContextType | undefined>(undefined);

// eslint-disable-next-line react-refresh/only-export-components
export const usePage = (): PageContextType => {
    const context = useContext(PageContext);
    if (!context) {
        throw new Error("usePage must be used within a PageProvider");
    }
    return context;
};

// Провайдер для контекста
export const PageProvider = ({ children }: { children: ReactNode }) => {
    const [currentPage, setCurrentPage] = useState<Page>("MAIN");

    return (
        <PageContext.Provider value={{ currentPage, setCurrentPage }}>
            {children}
        </PageContext.Provider>
    );
};
