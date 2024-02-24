import { Fragment, useState } from 'react'
import { Listbox, Transition } from '@headlessui/react'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid'

const postTypes = [
  { id: 1, name: 'Hot', value: 'hot' },
  { id: 2, name: 'New', value: 'new' },
  { id: 3, name: 'Controversial', value: 'controversial' },
  { id: 4, name: 'Rising', value: 'rising' },
  { id: 5, name: 'Top', value: 'top' },
]

export default function PostTypes({ selected, onPostTypeChange }) {
  return (
    <div className="w-full relative">
      <Listbox value={selected} onChange={onPostTypeChange}>
        <div className="relative mt-1">
          <Listbox.Button className="w-full relative field">
            <span className="block truncate">{selected.name}</span>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <ChevronUpDownIcon
                className="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
            </span>
          </Listbox.Button>
          <Transition
            as={Fragment}
            leave="transition ease-in duration-100"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm">
              {postTypes.map((postType, postTypeIdx) => (
                <Listbox.Option
                  key={postTypeIdx}
                  className={({ active }) =>
                    `relative cursor-default select-none py-2 pl-10 pr-4 ${
                      active ? 'bg-green-100 text-green-900' : 'text-gray-900'
                    }`
                  }
                  value={postType}
                >
                  {({ selected }) => (
                    <>
                      <span
                        className={`block truncate ${
                          selected ? 'font-medium' : 'font-normal'
                        }`}
                      >
                        {postType.name}
                      </span>
                      {selected ? (
                        <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600">
                          <CheckIcon className="h-5 w-5" aria-hidden="true" />
                        </span>
                      ) : null}
                    </>
                  )}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </Transition>
        </div>
      </Listbox>
    </div>
  )
}
