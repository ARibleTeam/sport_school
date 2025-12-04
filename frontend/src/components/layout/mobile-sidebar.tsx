import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Calendar, Users, Settings, LogOut, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MobileSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

interface NavItemProps {
  icon: React.ElementType;
  label: string;
  to: string;
  onClick?: () => void;
}

const NavItem: React.FC<NavItemProps> = ({ icon: Icon, label, to, onClick }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link 
      to={to} 
      onClick={onClick}
      className={cn(
        "flex items-center space-x-3 p-3 rounded-xl transition-colors duration-200 text-sm font-medium",
        "text-gray-500",
        "hover:bg-gray-100 hover:text-gray-900",
        isActive && "bg-gray-100 text-gray-900"
      )}
    >
      <Icon className="w-5 h-5 stroke-[1.5px]" /> 
      <span>{label}</span>
    </Link>
  );
};

export const MobileSidebar: React.FC<MobileSidebarProps> = ({ isOpen, onClose }) => {
  const navigationItems = [
    { icon: Home, label: "Dashboard", to: "/" },
    { icon: Calendar, label: "Расписание", to: "/schedule" },
    { icon: Users, label: "Тренеры", to: "/coaches" },
    { icon: Settings, label: "Настройки", to: "/settings" },
  ];

  // Блокируем скролл когда сайдбар открыт
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    // Очищаем стили при размонтировании
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Закрываем сайдбар по нажатию Escape
  React.useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  return (
    <>
      {/* Overlay */}
      <div 
        className={cn(
          "fixed inset-0 bg-black/50 z-40 lg:hidden transition-opacity duration-300",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onClose}
      />
      
      {/* Sidebar */}
      <div 
        className={cn(
          "fixed top-0 left-0 h-full w-[280px] z-50 lg:hidden",
          "bg-white border-r border-gray-200 shadow-xl",
          "transform transition-transform duration-300 ease-in-out",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">
            SPORT SCHOOL
          </h1>
          <button 
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5 stroke-[1.5px]" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex flex-col p-4 space-y-2 flex-grow">
          {navigationItems.map((item) => (
            <NavItem 
              key={item.to} 
              {...item} 
              onClick={onClose}
            />
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200">
          <NavItem 
            icon={LogOut} 
            label="Выйти" 
            to="/logout" 
            onClick={onClose}
          />
        </div>
      </div>
    </>
  );
};
