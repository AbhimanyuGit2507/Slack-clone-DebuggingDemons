import {
  Hash,
  Lock,
  MessageCircle,
  Users,
  Pencil,
  UserPlus,
  Mail,
  ChevronDown,
  ChevronRight,
  Sparkles,
  Phone,
  Folder,
  Star,
  Settings,
  Edit3,
  Plus,
  Search,
  FileText,
  List,
  Zap,
  Image as ImageIcon,
  Send,
  MoreVertical
} from 'lucide-react'
import { SiSlack } from 'react-icons/si'

// Export all icons with consistent naming
export const Icons = {
  // Channel related
  Hash,
  Lock,
  MessageCircle,
  Users,
  
  // Actions
  Pencil,
  Edit: Edit3,
  UserPlus,
  Mail,
  Plus,
  Send,
  Search,
  
  // Navigation
  ChevronDown,
  ChevronRight,
  MoreVertical,
  
  // Special
  Sparkles,
  Phone,
  Folder,
  Star,
  Settings,
  
  // Files
  FileText,
  List,
  Zap,
  ImageIcon,
  
  // Brand
  Slack: SiSlack
}

// Helper component for consistent icon styling
export const Icon = ({ name, size = 18, className = '', color = 'currentColor', ...props }) => {
  const IconComponent = Icons[name]
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`)
    return null
  }
  
  return <IconComponent size={size} color={color} className={className} {...props} />
}

export default Icons
