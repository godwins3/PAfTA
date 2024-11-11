import NextLink from 'next/link'
import { AnchorHTMLAttributes, ReactNode } from 'react'

interface Props extends AnchorHTMLAttributes<HTMLAnchorElement> {
    href: string;
    children: ReactNode;
}

export const Link = ({ children, href, ...props }: Props) => {
    return (
        <NextLink href={href} {...props}>
            {children}
        </NextLink>
    )
}