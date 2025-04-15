import { Outlet } from "react-router"
import { Header } from "@/components/global/info-bar"
import Footer from "@/components/global/footer"

const Layout = () => {
    return (
        <div className="w-full h-full">
            <Header toggleSidebar={() => { }} />
            <Outlet />
            <Footer/>
            {/* <Sidebar isOpen={false} onClose={() => {}} /> */}
        </div>
    )
}

export default Layout