import "./App.css";
import Header from "./components/Header/Header";
import MainPage from "./MainPage/MainPage";
import { usePage } from "./Contexts/PageContext/PageContext";
import InterfacePage from "./InterfacePage/InterfacePage";
function App() {
    const pageContext = usePage();
    const renderPage = () => {
        switch (pageContext.currentPage) {
            case "MAIN":
                return <MainPage />;
            case "INTERFACE":
                return <InterfacePage />;
            // case "PHOTOS":
            //     return <PhotosPage />;
            // case "HISTORY":
            //     return <HistoryPage />;
            // case "LOGIN":
            //     return <LoginPage />;
            default:
                return <MainPage />;
        }
    };

    return (
        <>
            <Header />
            {renderPage()}
        </>
    );
}

export default App;
