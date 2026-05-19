; ==============================================================
; DOMAIN: SATELLITE
; ==============================================================

(define (domain satellite-v3)

(:requirements
    :strips
    :typing
    :negative-preconditions
    :action-costs
)

(:types direction object quality level)

(:predicates

    (pointing ?d - direction)
    (next-right ?from - direction ?to - direction)
    (next-left ?from - direction ?to - direction)
    (is-north ?d - direction)

    (visible ?o - object ?d - direction)
    (required ?q - quality ?o - object)

    (stored ?q - quality ?o - object)

    (sent ?q - quality ?o - object)

    (captured ?o - object)

    (mem-free ?l - level)
    (mem-take ?q - quality ?from - level ?to - level)
    (mem-send ?q - quality ?from - level ?to - level)
)

(:functions
    (total-cost)
)

(:action rotate-right
 :parameters (?from - direction ?to - direction)
 :precondition (and
    (pointing ?from)
    (next-right ?from ?to)
 )
 :effect (and
    (not (pointing ?from))
    (pointing ?to)
    (increase (total-cost) 1)
 )
)

(:action rotate-left
 :parameters (?from - direction ?to - direction)
 :precondition (and
    (pointing ?from)
    (next-left ?from ?to)
 )
 :effect (and
    (not (pointing ?from))
    (pointing ?to)
    (increase (total-cost) 1)
 )
)

(:action take-picture
 :parameters (?q - quality ?o - object ?d - direction
              ?from - level ?to - level)
 :precondition (and
    (pointing ?d)
    (visible ?o ?d)
    (required ?q ?o)
    (not (captured ?o))
    (not (sent ?q ?o))
    (mem-free ?from)
    (mem-take ?q ?from ?to)
 )
 :effect (and
    (stored ?q ?o)
    (captured ?o)
    (not (mem-free ?from))
    (mem-free ?to)
    (increase (total-cost) 2)
 )
)

(:action send
 :parameters (?q - quality ?o - object ?n - direction
              ?from - level ?to - level)
 :precondition (and
    (pointing ?n)
    (is-north ?n)
    (stored ?q ?o)
    (required ?q ?o)
    (mem-free ?from)
    (mem-send ?q ?from ?to)
 )
 :effect (and
    (not (stored ?q ?o))
    (sent ?q ?o)
    (not (mem-free ?from))
    (mem-free ?to)
    (increase (total-cost) 2)
 )
)

)