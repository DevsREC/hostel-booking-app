import { Route, Routes } from "react-router";
import Profile from "./profile/page";
import Setting from "./setting/page";
import Hostels from "./hostels/page";
import HostelDetail from "./hostels/[id]/page";
import Bookings from "./bookings/page";
import BookingDetail from "./bookings/[id]/page";
import { ProtectedRoute } from "../../components/auth/protected-route";
import PageNotFound from "../page-not-found/page";

export default function Dashboard() {
  return (
    <ProtectedRoute>
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/setting" element={<Setting />} />
        <Route path="/" element={<Hostels />} />
        <Route path="/hostels/:id" element={<HostelDetail />} />
        <Route path="/bookings" element={<Bookings />} />
        <Route path="/bookings/:id" element={<BookingDetail />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </ProtectedRoute>
  );
} 