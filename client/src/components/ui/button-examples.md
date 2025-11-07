# Button Component Usage Guide

## Overview
The Button component now supports a separate `colorScheme` property that allows you to easily change button colors independently of the semantic `variant` prop.

## Properties

### `variant` (Semantic Styling)
Controls the button's visual style based on its purpose:
- `default` - Primary action button
- `destructive` - Dangerous/delete actions
- `outline` - Secondary outlined button
- `secondary` - Secondary solid button
- `ghost` - Minimal hover-only button
- `link` - Text link styled button

### `colorScheme` (Color Customization)
Controls the button's color independently:
- `default` - Uses variant's default color
- `primary` - Primary theme color
- `secondary` - Secondary theme color
- `destructive` - Red/destructive color
- `success` - Green color
- `warning` - Yellow color
- `info` - Blue color
- `purple` - Purple color
- `pink` - Pink color
- `indigo` - Indigo color
- `teal` - Teal color
- `orange` - Orange color
- `gray` - Gray color

### `size`
Controls the button's size:
- `default` - Standard height (h-9)
- `sm` - Small height (h-8)
- `lg` - Large height (h-10)
- `icon` - Square icon button (size-9)
- `icon-sm` - Small square icon (size-8)
- `icon-lg` - Large square icon (size-10)

## Usage Examples

### Basic Usage with Variant Only
```tsx
<Button variant="default">Default Button</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
```

### Using ColorScheme for Custom Colors
```tsx
// Success button with default variant
<Button colorScheme="success">Save Changes</Button>

// Warning button with default variant
<Button colorScheme="warning">Warning Action</Button>

// Info button with default variant
<Button colorScheme="info">Learn More</Button>

// Purple button
<Button colorScheme="purple">Premium Feature</Button>
```

### Combining Variant and ColorScheme
```tsx
// Outline button with custom color
<Button variant="outline" colorScheme="success">Approve</Button>

// Ghost button with custom color
<Button variant="ghost" colorScheme="info">Info</Button>
```

### Icon Buttons with ColorScheme
```tsx
<Button size="icon" colorScheme="success">
  <CheckIcon />
</Button>

<Button size="icon" colorScheme="destructive">
  <TrashIcon />
</Button>

<Button size="icon" colorScheme="info">
  <InfoIcon />
</Button>
```

### Different Sizes with ColorScheme
```tsx
<Button size="sm" colorScheme="teal">Small Button</Button>
<Button size="default" colorScheme="purple">Default Button</Button>
<Button size="lg" colorScheme="orange">Large Button</Button>
```

## Migration Guide

### Before (Using only variant)
```tsx
<Button variant="destructive">Delete</Button>
```

### After (Using colorScheme for more flexibility)
```tsx
// Keep using variant for semantic meaning
<Button variant="destructive">Delete</Button>

// Or use colorScheme for custom colors
<Button colorScheme="destructive">Delete</Button>
<Button colorScheme="success">Approve</Button>
<Button colorScheme="warning">Caution</Button>
```

## Notes
- When `colorScheme` is set to `"default"`, the button will use the color from the `variant` prop
- The `colorScheme` prop overrides the color styling from `variant` when specified
- Both props can be used together for maximum flexibility
- All color schemes include dark mode support
