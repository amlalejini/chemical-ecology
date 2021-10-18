//  This file is part of Artificial Ecology for Chemical Ecology Project
//  Copyright (C) Emily Dolson, 2021.
//  Released under MIT license; see LICENSE

#include <iostream>

#include "emp/base/vector.hpp"

#include "chemical-ecology/config_setup.hpp"
#include "chemical-ecology/example.hpp"
#include "chemical-ecology/ExampleConfig.hpp"

// This is the main function for the NATIVE version of Artificial Ecology for Chemical Ecology Project.

chemical_ecology::Config cfg;

int main(int argc, char* argv[])
{ 
  // Set up a configuration panel for native application
  setup_config_native(cfg, argc, argv);
  cfg.Write(std::cout);

  std::cout << "Hello, world!" << "\n";

  return example();
}
